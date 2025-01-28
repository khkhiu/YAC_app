import React from "react";
import { View, Text, Image } from "react-native";
import { JournalCardProps } from "./types";

export const JournalCard: React.FC<JournalCardProps> = ({
  status,
  title,
  description,
  imageUrl,
  imageAlt,
}) => {
  return (
    <View className="relative px-4 py-3 mb-2 bg-white rounded-2xl border border-solid shadow-2xl border-neutral-200 max-sm:px-3 max-sm:py-2.5">
      <View className="flex gap-1 items-center px-2 py-0.5 text-xs font-semibold rounded-[999px] w-fit">
        <View />
        <View>
          <Text>{status}</Text>
        </View>
      </View>
      <View className="flex justify-between mt-3">
        <View className="flex-1">
          <View className="text-sm font-semibold text-neutral-950">
            <Text>{title}</Text>
          </View>
          <View className="mt-1 text-xs text-neutral-500">
            <Text>{description}</Text>
          </View>
        </View>
        <View>
          <Image
            source={{ uri: imageUrl }}
            accessibilityLabel={imageAlt}
            className="object-cover rounded-xl h-[52px] w-[52px]"
          />
        </View>
      </View>
      {status === "completed" && (
        <View className="absolute top-3 right-4 text-green-500" />
      )}
    </View>
  );
};
