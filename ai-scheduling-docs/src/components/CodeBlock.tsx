import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { useState } from "react";

interface CodeBlockProps {
  children: string;
  language?: string;
  title?: string;
}

export const CodeBlock = ({ children, language = "bash", title }: CodeBlockProps) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group">
      {title && (
        <div className="flex items-center justify-between bg-muted px-3 sm:px-4 py-2 rounded-t-lg border border-b-0">
          <span className="text-xs sm:text-sm font-medium text-muted-foreground">{title}</span>
          <span className="text-xs text-muted-foreground uppercase">{language}</span>
        </div>
      )}
      <div className="relative">
        <pre className={cn(
          "bg-code-bg text-foreground p-3 sm:p-4 overflow-x-auto text-xs sm:text-sm leading-relaxed",
          title ? "rounded-b-lg" : "rounded-lg",
          "border border-border"
        )}>
          <code className="text-ai-cyan">{children}</code>
        </pre>
        <Button
          variant="ghost"
          size="sm"
          className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 sm:h-8 sm:w-8 p-0"
          onClick={copyToClipboard}
        >
          {copied ? (
            <Check className="h-3 w-3 sm:h-4 sm:w-4 text-accent" />
          ) : (
            <Copy className="h-3 w-3 sm:h-4 sm:w-4" />
          )}
        </Button>
      </div>
    </div>
  );
};

// Helper function for className
function cn(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}