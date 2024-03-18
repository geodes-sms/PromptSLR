import React from "react";
import "./styles.scss";

const Button = (props: {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  isLoading?: boolean;
}) => {
  return (
    <button
      className={`custom-button ${props.disabled && "custom-button__disabled"}`}
      onClick={props.onClick}
    >
      {props.label}
    </button>
  );
};

export default Button;
