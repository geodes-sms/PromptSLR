import React from "react";
import "./styles.scss";

function NavItem(props: {
  key: string | number;
  isSelected: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <li
      key={props.key}
      className={`navItem ${props.isSelected && "navItem--selected"}`}
      onClick={props.onClick}
    >
      {props.label}
    </li>
  );
}

export default NavItem;
