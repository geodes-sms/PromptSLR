import React, { useEffect, useState } from "react";
import "./styles.scss";
import NavItem from "../NavItem/NavItem";
import { useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  const [selectedTabIndex, setSelectedTabIndex] = useState(-1);

  useEffect(() => {
    onUpdateSelectedTabBasedOnPath();
  }, [location.pathname]);

  const onUpdateSelectedTabBasedOnPath = () => {
    const selectedIdx = navbar_items.findIndex(
      (item) => item.link === location.pathname
    );
    if (selectedIdx >= 0) setSelectedTabIndex(selectedIdx);
  };

  const navbar_items = [
    {
      key: 1,
      label: "Configuration",
      link: "/",
    },
    {
      key: 2,
      label: "Results",
      link: "/results",
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
              link={item.link}
              onClick={() => ScrollToSection(i)}
            />
          );
        })}
      </ul>
    </nav>
  );
}

export default Navbar;
