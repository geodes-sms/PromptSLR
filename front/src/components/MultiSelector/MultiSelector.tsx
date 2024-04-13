import React, { useState } from "react";
import "./styles.scss";
import SVGIcon from "../SVGIcon/SVGIcon";

const MultiSelector = (props: {
  label: string;
  dropdownItems: string[];
  selectedItems: string[];
  setSelectedItems: (item: string[]) => void;
}) => {
  const { selectedItems, setSelectedItems } = props;

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // const [selectedItems, setSelectedItems] = useState<string[]>([]);

  const handleItemSelect = (e: any, item: string) => {
    e.stopPropagation();
    !selectedItems.includes(item) && setSelectedItems([...selectedItems, item]);
  };

  const handleItemRemove = (e: any, item: string) => {
    e.stopPropagation();
    setSelectedItems(selectedItems.filter((element) => element != item));
  };

  const createDropDownItemsUI = () => {
    const { dropdownItems } = props;
    let dropDownItemsUI = [];
    for (let i = 0; i < dropdownItems.length; i++) {
      dropDownItemsUI.push(
        <div
          key={i}
          className={`multi-select-item
            ${isDropdownOpen && "multi-select-item-active"} ${
            selectedItems.includes(dropdownItems[i]) &&
            "multi-select-item--selected"
          }`}
          onClick={(e) => handleItemSelect(e, dropdownItems[i])}
        >
          <span className="multi-select-text">{dropdownItems[i]}</span>
        </div>
      );
    }
    return dropDownItemsUI;
  };

  const selectedItemBox = (item: string, index: number) => {
    return (
      <div className="multi-select-selector-selected-item-box" key={index}>
        <span>{item}</span>
        <div
          className="multi-select-selector-selected-item-box__remove"
          onClick={(e) => handleItemRemove(e, item)}
        >
          <SVGIcon name="cross" width={"18"} height={"18"} fill="#fff" />
        </div>
      </div>
    );
  };

  return (
    <div className="multi-select-selector-container">
      <p className="multi-select-selector-label">{props.label}</p>
      <div
        className="multi-select-selection-button"
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
      >
        <div
          className="multi-select-title"
          style={{
            color: "#1e1e20",
          }}
        >
          {"Select"}
        </div>
        <div className="multi-select-arrow-container">
          <SVGIcon
            name="arrowDown"
            width={"18"}
            height={"18"}
            className={`arrow-icon
          ${isDropdownOpen && "arrow-icon-active"}`}
          />
        </div>
        <div
          className={`multi-select-items-container
           ${isDropdownOpen && "multi-select-items-container-active"}`}
        >
          {selectedItems.length > 0 && (
            <div className="multi-select-selected-items">
              {selectedItems.map((item, i) => {
                return selectedItemBox(item, i);
              })}
            </div>
          )}
          {createDropDownItemsUI()}
        </div>
      </div>
    </div>
  );
};

export default MultiSelector;
