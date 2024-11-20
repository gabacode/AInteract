import { PostType } from "../../../types";
import { timesAgo } from "./utils";
import "./index.scss";

// Main Post Component
interface PostProps {
  post: PostType;
  deletePost: (postId: number) => void;
}

export const Post = ({ post, deletePost }: PostProps) => {
  const handleDelete = () => {
    deletePost(post.id!);
  };

  return (
    <div className="post card">
      <div className="row align-items-start">
        <div className="col-auto pe-0">
          <Avatar src={post.author.avatar || ""} alt={post.author.username} />
        </div>
        <div className="col">
          <AuthorDetails
            username={post.author.username}
            isAi={post.author.is_ai}
            timestamp={post.timestamp}
          />
          <PostContent content={post.content} />
        </div>
        <div className="col-auto text-end">
          <DropdownActions onDelete={handleDelete} postId={post.id!} />
        </div>
      </div>
    </div>
  );
};

// Avatar Component
const Avatar = ({ src, alt }: { src: string; alt: string }) => (
  <img className="avatar" src={src} alt={alt} />
);

// AuthorDetails Component
interface AuthorDetailsProps {
  username: string;
  isAi: boolean;
  timestamp: string;
}

const AuthorDetails = ({ username, isAi, timestamp }: AuthorDetailsProps) => {
  const classes = `badge ${isAi ? "badge-ai" : "badge-human"}`;
  return (
    <small>
      <b>
        {username} <span className={classes}>{isAi ? "AI" : "HUMAN"}</span>
      </b>{" "}
      {timesAgo(timestamp)}
    </small>
  );
};

// PostContent Component
interface PostContentProps {
  content: string;
}
const PostContent = ({ content }: PostContentProps) => <p>{content}</p>;

// DropdownActions Component
interface DropdownActionsProps {
  onDelete: () => void;
  postId: number;
}
const DropdownActions = ({ onDelete, postId }: DropdownActionsProps) => (
  <div className="dropdown">
    <button
      className="btn btn-light btn-sm dropdown-toggle"
      type="button"
      id={`dropdownMenuButton${postId}`}
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      ...
    </button>
    <ul
      className="dropdown-menu"
      aria-labelledby={`dropdownMenuButton${postId}`}
    >
      <li>
        <button className="dropdown-item text-danger" onClick={onDelete}>
          Delete
        </button>
      </li>
    </ul>
  </div>
);
