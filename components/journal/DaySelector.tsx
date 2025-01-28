import React from "react";
import { View, Text } from "react-native";
import { DayProps } from "./types";

const days: DayProps[] = [
  { day: "M", date: "29" },
  { day: "T", date: "30", isActive: true },
  { day: "W", date: "01" },
  { day: "T", date: "02" },
  { day: "F", date: "03" },
  { day: "S", date: "04" },
  { day: "S", date: "05" },
];

export const DaySelector: React.FC = () => {
  return (
    <View className="flex justify-between px-4 py-0 max-sm:px-2 max-sm:py-0">
      {days.map((item, index) => (
        <View key={index} className="flex flex-col gap-2 items-center">
          <View className="text-sm text-neutral-950">
            <Text>{item.day}</Text>
          </View>
          <View
            className={`text-base font-semibold h-[30px] rounded-[999px] w-[30px] ${
              item.isActive
                ? "text-white bg-rose-400 shadow-[0_2px_4px_rgba(0,0,0,0.1)]"
                : ""
            }`}
          >
            <Text>{item.date}</Text>
          </View>
        </View>
      ))}
    </View>
  );
};
