import "./index.scss";

interface AvatarProps {
  src?: string;
  alt: string;
}

export const Avatar = ({ src, alt }: AvatarProps) => (
  <img className="avatar" src={src || ""} alt={alt} />
);
