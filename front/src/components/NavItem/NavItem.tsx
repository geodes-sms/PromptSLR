import React from "react";
import "./styles.scss";
import { Routes, Route, Outlet, Link } from "react-router-dom";

function NavItem(props: {
  key: string | number;
  isSelected: boolean;
  label: string;
  link: string;
  onClick: () => void;
}) {
  return (
    <Link
      key={props.key}
      className={`navItem ${props.isSelected && "navItem--selected"}`}
      to={props.link}
      onClick={props.onClick}
    >
      {props.label}
    </Link>
  );
}

export default NavItem;
