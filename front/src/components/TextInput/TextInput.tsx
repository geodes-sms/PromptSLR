import React, { useEffect, useState } from "react";
import "./styles.scss";

const TextInput = (props: {
  label?: string;
  value: string;
  setValue: (item: string) => void;
  type?: string;
  min?: number;
  max?: number;
  step?: number;
  placeholder?: string;
  disabled?: boolean;
}) => {
  return (
    <div className="text-input">
      {!!props.label ? (
        <p className="text-input__label">{props.label}</p>
      ) : null}
      <input
        value={props.value}
        type={props.type ? props.type : "text"}
        onChange={(e) => props.setValue(e.target.value)}
        className="text-input__field"
        min={props.min}
        max={props.max}
        step={props.step}
        placeholder={props.placeholder}
        disabled={props.disabled}
      />
    </div>
  );
};

export default TextInput;
