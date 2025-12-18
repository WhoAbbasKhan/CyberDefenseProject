import { CheckCircle2, Circle, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface KillChainTimelineProps {
    currentStage: string;
    stages?: string[];
}

const DEFAULT_STAGES = [
    "Reconnaissance",
    "Weaponization",
    "Delivery",
    "Exploitation",
    "Installation",
    "C2",
    "Action"
];

export function KillChainTimeline({ currentStage, stages = DEFAULT_STAGES }: KillChainTimelineProps) {
    const currentIndex = stages.findIndex(s => s.toLowerCase() === currentStage.toLowerCase());
    // If not found, defaulting to -1 (none started) or handle as 'Unknown'

    return (
        <div className="w-full py-4">
            <div className="flex items-center justify-between relative">
                {/* Progress Bar Background */}
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-muted z-0 hidden md:block" />

                {/* Progress Bar Fill */}
                <div
                    className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-primary z-0 transition-all duration-500 hidden md:block"
                    style={{ width: `${(currentIndex / (stages.length - 1)) * 100}%` }}
                />

                {stages.map((stage, index) => {
                    const isCompleted = index <= currentIndex;
                    const isCurrent = index === currentIndex;

                    return (
                        <div key={stage} className="relative z-10 flex flex-col items-center group">
                            <div
                                className={cn(
                                    "w-8 h-8 rounded-full flex items-center justify-center border-2 bg-background transition-colors",
                                    isCompleted ? "border-primary bg-primary text-primary-foreground" : "border-muted-foreground text-muted-foreground",
                                    isCurrent && "ring-4 ring-primary/20 scale-110 border-primary"
                                )}
                            >
                                {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : <Circle className="w-5 h-5" />}
                            </div>
                            <span className={cn(
                                "absolute top-10 text-xs font-medium whitespace-nowrap transition-colors",
                                isCompleted ? "text-primary" : "text-muted-foreground",
                                isCurrent && "font-bold text-foreground"
                            )}>
                                {stage}
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
