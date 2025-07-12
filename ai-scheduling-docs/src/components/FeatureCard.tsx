import { Card, CardContent } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  className?: string;
}

export const FeatureCard = ({ icon: Icon, title, description, className }: FeatureCardProps) => {
  return (
    <Card className={cn(
      "group hover:shadow-lg transition-all duration-300 hover:-translate-y-1",
      "border-border/50 hover:border-accent/20 bg-card/50 backdrop-blur-sm",
      className
    )}>
      <CardContent className="p-4 sm:p-6">
        <div className="flex items-start gap-3 sm:gap-4">
          <div className="p-2 sm:p-3 rounded-lg bg-gradient-primary/10 border border-accent/20 flex-shrink-0">
            <Icon className="h-5 w-5 sm:h-6 sm:w-6 text-accent" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-foreground mb-1 sm:mb-2 group-hover:text-accent transition-colors text-sm sm:text-base">
              {title}
            </h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              {description}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};