import React, { useEffect, useState } from "react";
import "./styles.scss";
import SVGIcon from "../SVGIcon/SVGIcon";

const DropdownSelector = (props: {
  label: string;
  dropdownItems: string[];
  selectedItem: string;
  setSelectedItem: (item: string) => void;
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [dropDownTitle, setDropDownTitle] = useState(props.selectedItem);

  const handleItemSelect = (item: string) => {
    setDropDownTitle(item);
    props.setSelectedItem(item);
  };

  useEffect(() => {
    setDropDownTitle(props.selectedItem);
  }, [props.selectedItem]);

  const createDropDownItemsUI = () => {
    const { dropdownItems } = props;
    let dropDownItemsUI = [];
    for (let i = 0; i < dropdownItems.length; i++) {
      dropDownItemsUI.push(
        <div
          key={i}
          className={`dropdown-item
          ${isDropdownOpen && "dropdown-item-active"} ${
            dropdownItems[i] === dropDownTitle && "dropdown-item--selected"
          }`}
          onClick={() => handleItemSelect(dropdownItems[i])}
        >
          <span className="dropdown-text">{dropdownItems[i]}</span>
        </div>
      );
    }
    return dropDownItemsUI;
  };

  return (
    <div className="dropdown-selector-container">
      <p className="dropdown-selector-label">{props.label}</p>
      <div
        className="dropdown-selection-button"
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
      >
        <div
          className="dropdown-title"
          style={{
            color: "#1e1e20",
          }}
        >
          {dropDownTitle}
        </div>
        <div className="dropdown-arrow-container">
          <SVGIcon
            name="arrowDown"
            width={"18"}
            height={"18"}
            className={`arrow-icon
        ${isDropdownOpen && "arrow-icon-active"}`}
          />
        </div>
        <div
          className={`dropdown-items-container
         ${isDropdownOpen && "dropdown-items-container-active"}`}
        >
          {createDropDownItemsUI()}
        </div>
      </div>
    </div>
  );
};

export default DropdownSelector;
