import React, { useEffect, useState } from "react";
import "./styles.scss";

const TextArea = (props: {
  label?: string;
  value: string;
  setValue: (item: string) => void;
  placeholder?: string;
  disabled?: boolean;
  rows?: number;
  cols?: number;
}) => {
  return (
    <div className="text-area">
      {!!props.label ? <p className="text-area__label">{props.label}</p> : null}
      <textarea
        value={props.value}
        onChange={(e) => props.setValue(e.target.value)}
        className="text-area__field"
        placeholder={props.placeholder}
        disabled={props.disabled}
        rows={props.rows}
        cols={props.cols}
      />
    </div>
  );
};

export default TextArea;
