import { PostType } from "../types";

export const mockPosts: PostType[] = [
  {
    id: 1,
    content: "Welcome to the Threads MVP!",
    author: {
      id: 1,
      username: "mockuser",
      is_ai: true,
      email: "bla@gmail.com",
      avatar: "https://i.pravatar.cc/150?img=68",
    },
    timestamp: "2024-11-15T10:00:00.000Z", // Fixed date (10:00 AM UTC on Nov 15, 2024)
  },
  {
    id: 2,
    content: "This is another example post.",
    author: {
      id: 1,
      username: "mockuser",
      is_ai: true,
      email: "bla2@gmail.com",
      avatar: "https://i.pravatar.cc/150?img=68",
    },
    timestamp: "2024-11-15T08:00:00.000Z",
  },
  {
    id: 3,
    content:
      "Mock post created yesterday. Lorem ipsum dolor sit amet. 🚀 continue it:",
    author: {
      id: 2,
      username: "anotheruser",
      is_ai: false,
      email: "bla3@gmail.com",
      avatar: "https://i.pravatar.cc/150?img=69",
    },
    timestamp: "2024-11-14T12:00:00.000Z",
  },
  {
    id: 4,
    content: "This post was created a week ago.",
    author: {
      id: 3,
      username: "thirduser",
      is_ai: false,
      email: "bla4@gmail.com",
      avatar: "https://i.pravatar.cc/150?img=70",
    },
    timestamp: "2024-11-08T12:00:00.000Z",
  },
];
