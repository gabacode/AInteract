import "./index.scss";

import { BsThreeDots } from "react-icons/bs";
import { ActionItem } from "../../../types";

interface DropdownActionsProps {
  actions: ActionItem[];
  postId: number;
}

export const DropdownActions = ({ actions, postId }: DropdownActionsProps) => (
  <div className="dropdown">
    <button
      className="btn btn-light btn-sm dropdown-toggle"
      type="button"
      id={`dropdownMenuButton${postId}`}
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      <BsThreeDots />
    </button>
    <ul
      className="dropdown-menu"
      aria-labelledby={`dropdownMenuButton${postId}`}
    >
      {actions.map((action, index) => (
        <li key={index}>
          <button
            className={`dropdown-item ${action.className || ""}`}
            onClick={() => action.onClick(postId)}
          >
            {action.label}
          </button>
        </li>
      ))}
    </ul>
  </div>
);
