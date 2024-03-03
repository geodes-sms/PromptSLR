import React, { useState } from "react";
import "./styles.scss";
import NavItem from "../NavItem/NavItem";

function Navbar() {
  const [selectedTabIndex, setSelectedTabIndex] = useState(0);

  const navbar_items = [
    {
      key: 1,
      label: "Configuration",
      link: "configuration",
    },
    {
      key: 2,
      label: "Results",
      link: "results",
    },
  ];

  const ScrollToSection = (index: number) => {
    setSelectedTabIndex(index);
    const tabDataDistances = navbar_items.map(
      (item) => document.getElementById(item.link)?.getBoundingClientRect().top
    );

    window.scrollBy({
      top: tabDataDistances[index],
      behavior: "smooth",
    });
  };

  return (
    <nav className="navbar">
      <ul className="navbar__list">
        {navbar_items.map((item, i) => {
          return (
            <NavItem
              key={item.key}
              isSelected={selectedTabIndex === i}
              label={item.label}
              onClick={() => ScrollToSection(i)}
            />
          );
        })}
      </ul>
    </nav>
  );
}

export default Navbar;
