import React, { useEffect, useState } from "react";
import "./styles.scss";

const TextInput = (props: {
  label: string;
  value: string;
  setValue: (item: string) => void;
  type?: string;
  min?: number;
  max?: number;
  step?: number;
  placeholder?: string;
}) => {
  return (
    <div className="text-input">
      <p className="text-input__label">{props.label}</p>
      <input
        value={props.value}
        type={props.type ? props.type : "text"}
        onChange={(e) => props.setValue(e.target.value)}
        className="text-input__field"
        min={props.min}
        max={props.max}
        step={props.step}
        placeholder={props.placeholder}
      />
    </div>
  );
};

export default TextInput;
