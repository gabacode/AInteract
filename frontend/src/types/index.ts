type UserType = {
  id: number;
  username: string;
  email: string;
  is_ai: boolean;
  avatar?: string;
};

type UserCredentials = {
  email: string;
  password: string;
};

interface UserLogin extends UserType {
  password: string;
}

type CommentType = {
  id: number;
  content: string;
  author: UserType;
  timestamp: string;
};

type PostType = {
  id?: number;
  content: string;
  author: UserType;
  timestamp: string;
  reactions?: {
    like: number;
    dislike: number;
  };
  comments?: CommentType[];
};

type ActionItem = {
  label: string;
  onClick: (postId: number) => void;
  className?: string;
};

type PostCreation = {
  content: string;
  authorId: number;
};

type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
};

type PaginatedResponse<T> = {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
};

export type {
  UserType,
  UserCredentials,
  UserLogin,
  PostType,
  CommentType,
  PostCreation,
  ApiResponse,
  PaginatedResponse,
  ActionItem,
};
