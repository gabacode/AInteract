import { Post } from "../../molecules/Post";
import { CreatePost } from "../../molecules/CreatePost";
import { useFeed } from "../../../hooks/useFeed";

import "./index.scss";

const Feed = () => {
  const { posts, addPost, deletePost, loading } = useFeed();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="feed">
      <CreatePost addPost={addPost} />
      {posts.results.map((post) => (
        <Post key={post.id} post={post} deletePost={deletePost} />
      ))}
    </div>
  );
};

export default Feed;
