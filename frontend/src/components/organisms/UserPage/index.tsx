import { useParams } from "react-router-dom";

export const UserPage = () => {
  const { username } = useParams();
  return (
    <div>
      <h1>Profile of {username}</h1>
    </div>
  );
};
