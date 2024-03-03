import React, { useState } from "react";
import "./styles.scss";
import NavItem from "../NavItem/NavItem";
import ConfigurationForm from "../ConfigurationForm/ConfigurationForm";
import JsonInput from "../JsonInput/JsonInput";

function ConfigurationWindow() {
  const [selectedConfigurationTab, setSelectedConfigurationTab] = useState(0);

  const tabs_data = [
    {
      key: 1,
      label: "Fill in the form",
      component: <ConfigurationForm />,
    },
    {
      key: 2,
      label: "Import JSON file",
      component: <JsonInput />,
    },
  ];
  return (
    <div className="config-window">
      <ul className="config-window__tabs">
        {tabs_data.map((item, i) => {
          return (
            <NavItem
              key={item.key}
              isSelected={selectedConfigurationTab === i}
              label={item.label}
              onClick={() => setSelectedConfigurationTab(i)}
            />
          );
        })}
      </ul>
      {tabs_data[selectedConfigurationTab].component}
    </div>
  );
}

export default ConfigurationWindow;
