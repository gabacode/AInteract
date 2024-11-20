import React, { useState } from "react";
import "./index.scss";

type CreatePostProps = {
  addPost: (content: string) => void;
};

export const CreatePost = ({ addPost }: CreatePostProps) => {
  const [content, setContent] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;
    addPost(content);
    setContent("");
  };

  return (
    <form className="create-post" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="What's on your mind?"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button type="submit">Post</button>
    </form>
  );
};
