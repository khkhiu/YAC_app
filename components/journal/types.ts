export interface DayProps {
  day: string;
  date: string;
  isActive?: boolean;
}

export interface JournalCardProps {
  status: "planned" | "completed";
  title: string;
  description: string;
  imageUrl: string;
  imageAlt: string;
}

export interface NavigationItemProps {
  icon: React.ReactNode;
  label: string;
  isActive?: boolean;
}
