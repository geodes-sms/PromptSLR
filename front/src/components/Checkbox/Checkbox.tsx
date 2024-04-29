import React from "react";
import "./styles.scss";

const Checkbox = (props: {
  isActive: boolean;
  setIsActive: (value: boolean) => void;
  label: string;
}) => {
  const { label, isActive, setIsActive } = props;

  const onToggle = (value: boolean) => {
    setIsActive(value);
  };
  return (
    <div className="checkbox-container">
      <p className="checkbox-label">{label}</p>
      <label className="checkbox">
        <input
          type="checkbox"
          checked={isActive}
          onChange={(e) => onToggle(e.target.checked)}
          className="checkbox-input"
        />
        <div className="checkbox-custom">
          <div
            className={`checkbox-custom-active-indicator ${
              isActive ? "active" : "inactive"
            }`}
          />
        </div>
      </label>
    </div>
  );
};

export default Checkbox;
