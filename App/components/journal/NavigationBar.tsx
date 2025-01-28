import React from "react";
import { View, Text } from "react-native";
import { NavigationItemProps } from "./types";

const navigationItems: NavigationItemProps[] = [
  { icon: <View />, label: "" },
  { icon: <View />, label: "" },
  { icon: <View />, label: "Journal", isActive: true },
  { icon: <View />, label: "" },
  { icon: <View />, label: "" },
];

export const NavigationBar: React.FC = () => {
  return (
    <View className="flex fixed bottom-0 justify-around px-0 py-4 w-full bg-white max-w-[375px]">
      {navigationItems.map((item, index) => (
        <View
          key={index}
          className="flex flex-col gap-1 items-center text-xs text-neutral-500"
        >
          {item.icon}
          {item.label && (
            <View>
              <Text>{item.label}</Text>
            </View>
          )}
        </View>
      ))}
    </View>
  );
};
