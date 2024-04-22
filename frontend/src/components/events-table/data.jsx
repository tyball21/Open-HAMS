import {
  CheckCircledIcon,
  CircleIcon,
  CrossCircledIcon,
  MinusCircledIcon,
  QuestionMarkCircledIcon,
  StopwatchIcon,
} from "@radix-ui/react-icons";

export const statuses = [
  {
    value: "check",
    label: "Pending Offer",
    icon: QuestionMarkCircledIcon,
  },
  {
    value: "active",
    label: "Active",
    icon: StopwatchIcon,
  },
  {
    value: "completed",
    label: "Completed",
    icon: CheckCircledIcon,
  },
  {
    value: "cancelled",
    label: "Cancelled",
    icon: CrossCircledIcon,
  },
  {
    value: "refunded",
    label: "Refunded",
    icon: MinusCircledIcon,
  },
  {
    value: "disputed",
    label: "Disputed",
    icon: CircleIcon,
  },
  {
    value: "late",
    label: "Late",
    icon: CircleIcon,
  },
];
