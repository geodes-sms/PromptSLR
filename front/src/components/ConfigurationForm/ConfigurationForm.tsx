import React, { useState } from "react";
import "./styles.scss";
import DropdownSelector from "../DropdownSelector/DropdownSelector";

function ConfigurationForm() {
  const [LLMName, setLLMName] = useState("");
  return (
    <div>
      <DropdownSelector
        dropdownItems={["ChatGPT", "Trainable", "Custom URL"]}
        selectedItem={LLMName}
        setSelectedItem={setLLMName}
      />
    </div>
  );
}

export default ConfigurationForm;
