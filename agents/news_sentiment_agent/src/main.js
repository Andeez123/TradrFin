import { Actor } from 'apify';
import { CheerioCrawler } from 'crawlee';
import Anthropic from '@anthropic-ai/sdk';

await Actor.init();

// Get input from the actor input (or use defaults if null)
const input = await Actor.getInput() || {};

const {
    query = 'NVIDIA',
    maxNewsItems = 10,
    maxSocialItems = 20,
    includeSocial = true,
    maxDaysOld = 7, // Default: only articles from last 7 days
} = input;

console.log(`🔍 Starting data collection for query: "${query}"`);
console.log(`📰 Max news items: ${maxNewsItems}`);
console.log(`🐦 Max social items: ${maxSocialItems}`);
console.log(`📅 Max article age: ${maxDaysOld} days`);

// Storage for collected data
const newsItems = [];
const socialPosts = [];

// Initialize limited arrays (will be populated or remain empty)
let limitedNews = [];
let limitedSocial = [];

// ============================================
// PART 1: Collect Financial News
// ============================================
console.log('\n📰 Collecting financial news...');

// Helper function to parse RSS date and check if it's within the time window
const isWithinDateRange = (pubDateString) => {
    if (!pubDateString) return false;

    try {
        // Parse RSS date format: "Fri, 05 Dec 2025 13:32:00 GMT"
        const articleDate = new Date(pubDateString);
        const now = new Date();
        const maxAge = maxDaysOld * 24 * 60 * 60 * 1000; // Convert days to milliseconds

        // Check if article is within the time window
        const age = now - articleDate;
        return age >= 0 && age <= maxAge;
    } catch (error) {
        // If date parsing fails, exclude the article to be safe
        console.log(`   ⚠️  Could not parse date: ${pubDateString}`);
        return false;
    }
};

// Helper function to parse RSS items
const parseRssItems = ($, items, sourceName, maxItems) => {
    const parsed = [];
    let skippedOld = 0;

    items.each((index, element) => {
        if (parsed.length >= maxItems) return false; // Stop if we have enough

        const $item = $(element);
        const title = $item.find('title').text().trim();
        const link = $item.find('link').text().trim();
        const pubDate = $item.find('pubDate').text().trim();
        const source = $item.find('source').text().trim() || sourceName || 'Unknown';
        const description = $item.find('description').text().trim();

        if (title) {
            // Check if article is within date range
            if (!isWithinDateRange(pubDate)) {
                skippedOld++;
                return; // Skip this article
            }

            // Clean HTML entities from description
            const cleanDescription = description
                .replace(/<[^>]*>/g, '') // Remove HTML tags
                .replace(/&[^;]+;/g, ' ') // Remove HTML entities
                .trim();

            parsed.push({
                title: title,
                url: link,
                source: source,
                publishedAt: pubDate || new Date().toISOString(),
                description: cleanDescription.substring(0, 500), // First 500 chars for better context
                content_length: cleanDescription.length,
                has_content: cleanDescription.length > 50 // Flag if we have substantial content
            });
        }
    });

    if (skippedOld > 0) {
        console.log(`   ⏭️  Skipped ${skippedOld} articles older than ${maxDaysOld} days`);
    }

    return parsed;
};

try {
    // Source 1: Google News RSS feed
    const googleNewsRssUrl = `https://news.google.com/rss/search?q=${encodeURIComponent(query + ' finance stock market')}&hl=en-US&gl=US&ceid=US:en`;

    console.log(`   📰 Fetching from Google News RSS...`);

    const googleNewsCrawler = new CheerioCrawler({
        async requestHandler({ $, request }) {
            console.log(`   Processing: ${request.url}`);

            const items = $('item');
            const parsed = parseRssItems($, items, 'Google News', Math.floor(maxNewsItems * 0.6)); // 60% from Google News

            newsItems.push(...parsed);
            console.log(`   ✅ Collected ${parsed.length} articles from Google News`);
        },
    });

    await googleNewsCrawler.run([googleNewsRssUrl]);

    // Source 2: Reuters RSS feed (Financial News)
    const googleNewsCount = newsItems.length;
    if (newsItems.length < maxNewsItems) {
        console.log(`   📰 Fetching from Reuters RSS...`);

        // Reuters has multiple financial feeds - using business news feed
        const reutersRssUrl = `https://www.reuters.com/rssFeed/businessNews`;

        // For stock-specific, we'll use the general business feed and filter by query in description
        const reutersCrawler = new CheerioCrawler({
            async requestHandler({ $, request }) {
                console.log(`   Processing: ${request.url}`);

                const items = $('item');

                // Parse all items and filter by query relevance and date
                let skippedOld = 0;
                items.each((index, element) => {
                    if (newsItems.length >= maxNewsItems) return false;

                    const $item = $(element);
                    const title = $item.find('title').text().trim();
                    const description = $item.find('description').text().trim();
                    const pubDate = $item.find('pubDate').text().trim();

                    // Filter for relevance to query (case-insensitive)
                    const searchText = (title + ' ' + description).toLowerCase();
                    const queryLower = query.toLowerCase();

                    // Check if article is within date range
                    if (!isWithinDateRange(pubDate)) {
                        skippedOld++;
                        return; // Skip this article
                    }

                    if (title && searchText.includes(queryLower)) {
                        const link = $item.find('link').text().trim();

                        const cleanDescription = description
                            .replace(/<[^>]*>/g, '')
                            .replace(/&[^;]+;/g, ' ')
                            .trim();

                        newsItems.push({
                            title: title,
                            url: link,
                            source: 'Reuters',
                            publishedAt: pubDate || new Date().toISOString(),
                            description: cleanDescription.substring(0, 500),
                            content_length: cleanDescription.length,
                            has_content: cleanDescription.length > 50
                        });
                    }
                });

                if (skippedOld > 0) {
                    console.log(`   ⏭️  Skipped ${skippedOld} Reuters articles older than ${maxDaysOld} days`);
                }

                const reutersCount = newsItems.length - googleNewsCount;
                console.log(`   ✅ Collected ${reutersCount} articles from Reuters`);
            },
        });

        await reutersCrawler.run([reutersRssUrl]);
    }

    // Limit to maxNewsItems
    limitedNews = newsItems.slice(0, maxNewsItems);
    console.log(`✅ Total news articles collected: ${limitedNews.length}`);

    // Show source breakdown
    const sourceBreakdown = {};
    limitedNews.forEach(item => {
        sourceBreakdown[item.source] = (sourceBreakdown[item.source] || 0) + 1;
    });
    console.log(`   Sources: ${Object.entries(sourceBreakdown).map(([s, c]) => `${s} (${c})`).join(', ')}`);

} catch (error) {
    console.error(`❌ Error collecting news: ${error.message}`);
    console.error(`   Stack: ${error.stack}`);
    limitedNews = []; // Ensure it's defined even on error
}

// ============================================
// PART 2: Collect Social Sentiment from Trusted News Sources
// ============================================
if (includeSocial) {
    console.log('\n📰 Collecting social sentiment from trusted news sources...');

    try {
        // Strategy: Get additional news articles with engagement metrics from trusted sources
        // We'll use Yahoo Finance, which has community engagement data

        console.log(`   📊 Fetching from Yahoo Finance for ${query}...`);

        const yahooFinanceUrl = `https://finance.yahoo.com/quote/${encodeURIComponent(query)}/community`;

        const socialCrawler = new CheerioCrawler({
            async requestHandler({ $, request }) {
                console.log(`   Processing: ${request.url}`);

                try {
                    // Yahoo Finance community section has discussions
                    const discussions = [];

                    // Try to find discussion posts or comments
                    let skippedOld = 0;
                    $('[data-test-locator="mega"], .comment, .discussion-item, article').each((i, element) => {
                        if (discussions.length >= maxSocialItems) return false;

                        const $item = $(element);
                        const text = $item.find('p, .comment-text, .discussion-text, [data-test="comment"]').first().text().trim();
                        const author = $item.find('.author, .username, [data-test="author"]').first().text().trim();
                        const time = $item.find('time, .timestamp, [data-test="timestamp"]').first().attr('datetime') ||
                            $item.find('time, .timestamp').first().text().trim();
                        const likes = parseInt($item.find('[aria-label*="like"], .like-count, [data-test="like"]').first().text().match(/\d+/)?.[0] || '0');

                        if (text && text.length > 20) { // Only include substantial comments
                            // Check if post is within date range
                            if (!isWithinDateRange(time)) {
                                skippedOld++;
                                return; // Skip this post
                            }

                            discussions.push({
                                text: text.substring(0, 500), // Limit length
                                likes: likes,
                                retweets: 0,
                                createdAt: time || new Date().toISOString(),
                                source: 'Yahoo Finance',
                                author: author || 'Anonymous'
                            });
                        }
                    });

                    if (skippedOld > 0) {
                        console.log(`   ⏭️  Skipped ${skippedOld} social posts older than ${maxDaysOld} days`);
                    }

                    if (discussions.length > 0) {
                        socialPosts.push(...discussions);
                        console.log(`   ✅ Collected ${discussions.length} discussions from Yahoo Finance`);
                    } else {
                        console.log(`   ⚠️  No discussions found on Yahoo Finance`);
                    }
                } catch (parseError) {
                    console.log(`   ⚠️  Error parsing Yahoo Finance: ${parseError.message}`);
                }
            },
        });

        await socialCrawler.run([yahooFinanceUrl]);

        // Fallback: Use news articles as sentiment indicators if no social data
        if (socialPosts.length === 0 && limitedNews.length > 0) {
            console.log(`   💡 Using news articles as sentiment indicators (trusted sources)`);

            // Convert news articles to social sentiment format
            limitedNews.forEach((news, index) => {
                if (socialPosts.length >= maxSocialItems) return;

                socialPosts.push({
                    text: news.title + (news.description ? ': ' + news.description : ''),
                    likes: 0, // News articles don't have likes
                    retweets: 0,
                    createdAt: news.publishedAt,
                    source: news.source,
                    author: news.source,
                    url: news.url,
                    type: 'news_article'
                });
            });

            limitedSocial = socialPosts.slice(0, maxSocialItems);
            console.log(`   ✅ Using ${limitedSocial.length} news articles as sentiment data`);
        } else if (socialPosts.length > 0) {
            limitedSocial = socialPosts.slice(0, maxSocialItems);
            console.log(`✅ Total social sentiment items collected: ${limitedSocial.length}`);
            console.log(`   Sources: ${[...new Set(limitedSocial.map(p => p.source))].join(', ')}`);
        } else {
            console.log(`   ⚠️  No social sentiment data collected from trusted sources`);
            console.log(`   💡 Note: Many financial sites require authentication or have anti-scraping measures`);
            console.log(`   💡 For production, consider using:`);
            console.log(`      - Financial news APIs (NewsAPI, Alpha Vantage)`);
            console.log(`      - Apify's financial news actors`);
            console.log(`      - RSS feeds with engagement metrics`);
            limitedSocial = [];
        }

    } catch (error) {
        console.error(`❌ Error collecting social sentiment: ${error.message}`);
        limitedSocial = [];
    }
} else {
    limitedSocial = [];
}

// ============================================
// PART 3: Analyze Sentiment with Claude
// ============================================
console.log('\n🧠 Analyzing sentiment with Claude...');

let sentimentAnalysis = null;

try {
    const anthropicApiKey = process.env.ANTHROPIC_API_KEY || Actor.getEnv().ANTHROPIC_API_KEY;

    if (!anthropicApiKey) {
        console.log('   ⚠️  ANTHROPIC_API_KEY not found. Skipping sentiment analysis.');
        console.log('   💡 Set ANTHROPIC_API_KEY in Apify actor environment variables or .env file');
    } else {
        const anthropic = new Anthropic({ apiKey: anthropicApiKey });

        // Prepare data for Claude
        const newsText = limitedNews.slice(0, 10).map((item, idx) =>
            `${idx + 1}. ${item.title}${item.description ? ': ' + item.description.substring(0, 200) : ''} (Source: ${item.source})`
        ).join('\n');

        const socialText = limitedSocial.slice(0, 10).map((item, idx) =>
            `${idx + 1}. ${item.text.substring(0, 200)} (Source: ${item.source})`
        ).join('\n');

        const prompt = `You are a financial sentiment analysis expert. Analyze the following financial news headlines and social sentiment data to determine market sentiment for "${query}".

NEWS HEADLINES:
${newsText || 'No news data available.'}

SOCIAL SENTIMENT:
${socialText || 'No social data available.'}

Please provide a comprehensive sentiment analysis in the following JSON format (respond ONLY with valid JSON, no markdown):
{
    "overall_sentiment": "positive|neutral|negative",
    "confidence_score": 0.0-1.0,
    "sector_sentiments": {
        "technology": "positive|neutral|negative",
        "finance": "positive|neutral|negative",
        "energy": "positive|neutral|negative"
    },
    "key_drivers": ["driver1", "driver2", "driver3"],
    "summary": "A 2-3 sentence summary of the market sentiment",
    "key_themes": ["theme1", "theme2", "theme3"],
    "risk_level": "low|medium|high"
}

Focus on:
1. Overall market mood (positive/neutral/negative)
2. Sector-level sentiment if mentioned
3. Key drivers (inflation, earnings, geopolitics, etc.)
4. Confidence based on data quality and consistency
5. Risk assessment based on conflicting signals

Respond ONLY with valid JSON, no additional text or markdown formatting.`;

        // Try different Claude models in order of preference
        const modelsToTry = [
            'claude-sonnet-4-5-20250929'
        ];

        let message = null;
        let lastError = null;

        for (const modelName of modelsToTry) {
            try {
                console.log(`   Trying model: ${modelName}`);
                message = await anthropic.messages.create({
                    model: modelName,
                    max_tokens: 1000,
                    messages: [{
                        role: 'user',
                        content: prompt
                    }]
                });
                console.log(`   ✅ Successfully used model: ${modelName}`);
                break; // Success, exit loop
            } catch (modelError) {
                lastError = modelError;
                console.log(`   ⚠️  Model ${modelName} failed: ${modelError.message}`);
                continue; // Try next model
            }
        }

        if (!message) {
            throw new Error(`All models failed. Last error: ${lastError?.message || 'Unknown error'}`);
        }

        // Extract JSON from Claude's response
        let responseText = message.content[0].text.trim();

        // Remove markdown code blocks if present
        if (responseText.includes('```json')) {
            responseText = responseText.split('```json')[1].split('```')[0].trim();
        } else if (responseText.includes('```')) {
            responseText = responseText.split('```')[1].split('```')[0].trim();
        }

        try {
            sentimentAnalysis = JSON.parse(responseText);
            console.log(`   ✅ Sentiment analysis complete`);
            console.log(`   Overall Sentiment: ${sentimentAnalysis.overall_sentiment?.toUpperCase() || 'UNKNOWN'}`);
            console.log(`   Confidence: ${sentimentAnalysis.confidence_score || 0}`);
        } catch (parseError) {
            console.log(`   ⚠️  Error parsing Claude response: ${parseError.message}`);
            console.log(`   Response preview: ${responseText.substring(0, 200)}...`);
            sentimentAnalysis = {
                overall_sentiment: 'neutral',
                confidence_score: 0.0,
                error: 'Failed to parse Claude response'
            };
        }
    }
} catch (error) {
    console.error(`   ❌ Error calling Claude: ${error.message}`);
    sentimentAnalysis = {
        overall_sentiment: 'neutral',
        confidence_score: 0.0,
        error: error.message
    };
}

// ============================================
// PART 4: Save Results
// ============================================
console.log('\n💾 Saving results...');

const output = {
    query: query,
    timestamp: new Date().toISOString(),
    data_sources: {
        news_count: limitedNews.length,
        social_count: limitedSocial.length,
    },
    news_items: limitedNews,
    social_posts: limitedSocial,
    sentiment_analysis: sentimentAnalysis,
    summary: {
        total_items: limitedNews.length + limitedSocial.length,
        data_quality: limitedNews.length >= 5 ? 'good' : 'limited',
        news_with_content: limitedNews.filter(n => n.has_content).length,
        sentiment_sources: limitedSocial.length > 0 ? [...new Set(limitedSocial.map(p => p.source))] : ['news_articles']
    }
};

// Save to default dataset
await Actor.pushData(output);

// Also save as key-value store for easy retrieval
await Actor.setValue('OUTPUT', output);

console.log(`\n✅ Data collection complete!`);
console.log(`   News items: ${limitedNews.length}`);
console.log(`   Social posts: ${limitedSocial.length}`);
console.log(`   Total items: ${output.summary.total_items}`);

await Actor.exit();
