import { Link } from "react-router-dom";
import { timesAgo } from "../../molecules/Post/utils";

import "./index.scss";

interface AuthorDetailsProps {
  username: string;
  isAi: boolean;
  timestamp: string;
}

export const AuthorDetails = ({
  username,
  isAi,
  timestamp,
}: AuthorDetailsProps) => {
  const classes = `badge ${isAi ? "badge-ai" : "badge-human"}`;
  return (
    <small>
      <b>
        <Link to={`/${username}`}>{username}</Link>{" "}
        <span className={classes}>{isAi ? "AI" : "HUMAN"}</span>
      </b>{" "}
      {timesAgo(timestamp)}
    </small>
  );
};
