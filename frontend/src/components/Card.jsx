import React from 'react';

const Card = ({ children, className = "", glow = "purple" }) => {
  const glowMap = {
    purple: "hover:shadow-glow-purple",
    green: "hover:shadow-glow-green",
    red: "hover:shadow-glow-red",
    none: ""
  };

  return (
    <div className={`bg-fintech-card border border-fintech-border rounded-[20px] p-6 transition-all duration-300 ${glowMap[glow]} ${className}`}>
      {children}
    </div>
  );
};

export default Card;