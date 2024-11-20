import { ActionItem, CommentType, PostType } from "../../../types";
import { Comments } from "../Comments";
import { Avatar } from "../../atoms/Avatar";
import { AuthorDetails } from "../../atoms/AuthorDetails";
import { PostContent } from "../../atoms/PostContent";
import { DropdownActions } from "../../atoms/DropdownActions";

import "./index.scss";

interface PostProps {
  post: PostType;
  actions: ActionItem[];
  fetchComments: (postId: number) => Promise<CommentType[]>;
  addComment: (
    postId: number,
    content: string,
    authorId: number
  ) => Promise<CommentType>;
}

export const Post = ({
  post,
  actions,
  fetchComments,
  addComment,
}: PostProps) => {
  return (
    <div className="post">
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
          {post.id && (
            <Comments
              postId={post.id}
              fetchComments={fetchComments}
              addComment={addComment}
            />
          )}
        </div>
        <div className="col-auto text-end">
          <DropdownActions actions={actions} postId={post.id!} />
        </div>
      </div>
    </div>
  );
};
