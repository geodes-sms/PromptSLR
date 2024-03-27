import React, { useEffect, useState } from "react";
import "./styles.scss";
import TextInput from "../TextInput/TextInput";
import SVGIcon from "../SVGIcon/SVGIcon";

const AddableKeyValueInput = (props: { title: string }) => {
  const [data, setData] = useState([
    { key: "", value: "", id: crypto.randomUUID() },
  ]);

  const updateData = (
    updatedIndex: number,
    updatedKey: "key" | "value",
    text: string
  ) => {
    const newData = [...data];
    newData[updatedIndex][updatedKey] = text;
    setData(newData);
  };

  const addField = () => {
    const newData = [...data];
    newData.push({ key: "", value: "", id: crypto.randomUUID() });
    setData(newData);
  };

  const removeField = (index: number) => {
    const newData = [...data];
    newData.splice(index, 1);
    setData(newData);
  };

  useEffect(() => {
    console.log("*** data changed:", data);
  }, [JSON.stringify(data)]);

  const renderKeyValuePairInput = (index: number) => {
    return (
      <div className="addable-inputs__row" key={data[index].id}>
        <TextInput
          label={"Key"}
          value={data[index].key}
          setValue={(text) => updateData(index, "key", text)}
          placeholder={`Key${index + 1}`}
        />
        <TextInput
          label={"Value"}
          value={data[index].value}
          setValue={(text) => updateData(index, "value", text)}
          placeholder={`Value${index + 1}`}
        />
        {data.length > 1 ? (
          <div
            className="addable-inputs__modify-btn"
            onClick={() => removeField(index)}
          >
            <SVGIcon name="minus" width={"20"} height={"20"} fill={"#D20F39"} />
          </div>
        ) : null}
        {index === data.length - 1 ? (
          <div className="addable-inputs__modify-btn" onClick={addField}>
            <SVGIcon name="plus" width={"20"} height={"20"} fill={"#40A02B"} />
          </div>
        ) : null}
      </div>
    );
  };

  return (
    <div className="addable-inputs">
      <p className="addable-inputs__title">{props.title}</p>
      {data.map((item, i) => {
        return renderKeyValuePairInput(i);
      })}
    </div>
  );
};

export default AddableKeyValueInput;
