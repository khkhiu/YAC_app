import React from "react";
import { View, Text } from "react-native";
import { DaySelector } from "./DaySelector";
import { JournalCard } from "./JournalCard";
import { NavigationBar } from "./NavigationBar";

const journalEntries = [
  {
    status: "planned" as const,
    title: "Eat Dry Ramen",
    description: "Make a dry ramen vegan for dinner",
    imageUrl: "https://placehold.co/52x52/f4d03f/f4d03f",
    imageAlt: "Ramen",
  },
  {
    status: "completed" as const,
    title: "Pumpkin Chicken Curry",
    description: "Make for a lunch time",
    imageUrl: "https://placehold.co/52x52/e67e22/e67e22",
    imageAlt: "Curry",
  },
  {
    status: "completed" as const,
    title: "Running 4K",
    description: "Exercise running at park center",
    imageUrl: "https://placehold.co/52x52/3498db/3498db",
    imageAlt: "Running",
  },
];

export const JournalScreen: React.FC = () => {
  return (
    <View className="relative mx-auto my-0 min-h-screen bg-white max-w-[375px] max-sm:w-full">
      <View className="flex justify-between px-5 py-2.5">
        <View className="font-semibold">
          <Text>9:41</Text>
        </View>
        <View className="flex gap-2">
          <View />
          <View />
        </View>
      </View>
      <View className="bg-rose-50 min-h-[calc(100vh_-_40px)] rounded-[24px_24px_0_0]">
        <View className="px-4 py-5 bg-rose-50">
          <View className="flex justify-between items-center mb-5">
            <View className="text-lg font-bold text-neutral-950">
              <Text>Journal</Text>
            </View>
            <View className="flex gap-3 items-center">
              <View className="flex p-1 bg-white border border-rose-400 border-solid rounded-[999px]">
                <View className="px-4 py-1 text-sm cursor-pointer rounded-[999px] text-neutral-500">
                  <Text>Day</Text>
                </View>
                <View className="px-4 py-1 text-sm cursor-pointer rounded-[999px] text-neutral-500">
                  <Text>Week</Text>
                </View>
              </View>
              <View className="flex justify-center items-center w-9 h-9 border border-rose-400 border-solid rounded-[999px]">
                <View />
              </View>
            </View>
          </View>
          <DaySelector />
        </View>
        <View className="p-4 bg-white">
          {journalEntries.map((entry, index) => (
            <JournalCard key={index} {...entry} />
          ))}
        </View>
        <View className="flex fixed right-4 justify-center items-center w-14 h-14 text-white bg-rose-400 cursor-pointer bottom-[90px] rounded-[999px] shadow-[0_2px_8px_rgba(0,0,0,0.1)] max-sm:right-3">
          <View />
        </View>
        <NavigationBar />
        <View className="mx-auto my-2 bg-neutral-950 h-[5px] rounded-[100px] w-[134px]" />
      </View>
    </View>
  );
};
