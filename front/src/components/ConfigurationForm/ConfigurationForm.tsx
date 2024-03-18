import React, { useState } from "react";
import "./styles.scss";
import DropdownSelector from "../DropdownSelector/DropdownSelector";
import TextInput from "../TextInput/TextInput";

function ConfigurationForm() {
  const [LLMName, setLLMName] = useState("");
  const [APIKey, setAPIKey] = useState("");
  const [temperature, setTemperature] = useState("0.2");

  return (
    <div>
      <DropdownSelector
        label={"LLM Name"}
        dropdownItems={["ChatGPT", "Trainable", "Custom URL"]}
        selectedItem={LLMName}
        setSelectedItem={setLLMName}
      />
      <TextInput value={APIKey} setValue={setAPIKey} label="API Key" />
      <TextInput
        value={temperature}
        setValue={setTemperature}
        label="Temperature"
        type="number"
        min={0}
        max={1}
        step={0.1}
      />
    </div>
  );
}

export default ConfigurationForm;
