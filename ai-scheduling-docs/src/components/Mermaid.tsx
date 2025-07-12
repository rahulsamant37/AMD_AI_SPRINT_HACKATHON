// src/components/Mermaid.tsx

import { useState, useEffect, useRef, FC } from "react";
import type { Mermaid } from "mermaid"; // Import only the type definitions

interface MermaidProps {
  chart: string;
}

// Global flag to ensure we only initialize Mermaid once
declare global {
  interface Window {
    mermaidInitialized?: boolean;
  }
}

export const Mermaid: FC<MermaidProps> = ({ chart }) => {
  // 1. A state to track if we are on the client side
  const [isClient, setIsClient] = useState(false);
  // 2. A ref to get a direct handle on the container div
  const containerRef = useRef<HTMLDivElement>(null);

  // 3. This effect runs only once when the component mounts on the client
  useEffect(() => {
    setIsClient(true);
  }, []);

  // 4. This effect handles all the Mermaid logic
  useEffect(() => {
    // We only run this logic if we are on the client and the container exists
    if (!isClient || !containerRef.current) {
      return;
    }

    // 5. We dynamically import the mermaid library
    import("mermaid").then((mermaid) => {
      // 6. Initialize the library only once
      if (!window.mermaidInitialized) {
        mermaid.default.initialize({
          startOnLoad: false,
          theme: "dark",
          securityLevel: "loose",
          themeVariables: {
            background: "#1c1917",
            primaryColor: "#2c2826",
            primaryTextColor: "#fafaf9",
            lineColor: "#f5f5f4",
            secondaryColor: "#e11d48",
            accentColor: "#e11d48",
          },
        });
        window.mermaidInitialized = true;
      }
      
      // Clear any previous render
      containerRef.current!.innerHTML = "";
      
      // 7. Render the diagram into the container
      try {
        const id = `mermaid-graph-${Math.random().toString(16).slice(2)}`;
        mermaid.default.render(id, chart, (svgCode) => {
          if (containerRef.current) {
            containerRef.current.innerHTML = svgCode;
          }
        });
      } catch (error) {
        console.error("Failed to render Mermaid chart:", error);
        if (containerRef.current) {
          containerRef.current.innerHTML = "Error rendering diagram.";
        }
      }
    });
  }, [chart, isClient]); // Re-run if the chart content changes or when we switch to client-side

  // Render a placeholder on the server and on the initial client render
  return (
    <div 
      ref={containerRef} 
      style={{ minHeight: '200px', display: 'flex', justifyContent: 'center', alignItems: 'center' }} 
    />
  );
};