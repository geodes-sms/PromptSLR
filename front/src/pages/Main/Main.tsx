import React from "react";
import "./styles.scss";
import Navbar from "../../components/Navbar/Navbar";
import ConfigurationWindow from "../../components/ConfigurationWindow/ConfigurationWindow";

function Main() {
  return (
    <>
      <Navbar />
      <section
        className="section__config"
        id="configuration"
        style={{ backgroundColor: "pink" }}
      >
        <ConfigurationWindow />
        {/* {text} */}
      </section>
      <section id="results" style={{ backgroundColor: "orange" }}>
        {text}
      </section>
    </>
  );
}

export default Main;

const text = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Volutpat sed cras ornare arcu dui vivamus arcu. Malesuada pellentesque elit eget gravida. Tincidunt dui ut ornare lectus. Aliquam ut porttitor leo a diam sollicitudin tempor. Ut lectus arcu bibendum at varius vel pharetra vel turpis. Mattis molestie a iaculis at erat pellentesque. Vulputate ut pharetra sit amet aliquam id diam maecenas ultricies. Potenti nullam ac tortor vitae purus faucibus ornare suspendisse. Gravida quis blandit turpis cursus in hac habitasse platea. Eu non diam phasellus vestibulum lorem sed risus. Auctor urna nunc id cursus metus aliquam eleifend mi in. Dui vivamus arcu felis bibendum ut. Tempus quam pellentesque nec nam aliquam sem.

Vel pretium lectus quam id leo. Placerat orci nulla pellentesque dignissim enim sit. Sed odio morbi quis commodo odio aenean sed adipiscing. Tincidunt nunc pulvinar sapien et ligula ullamcorper. Elementum sagittis vitae et leo duis ut. Volutpat est velit egestas dui. Egestas tellus rutrum tellus pellentesque eu tincidunt. Purus viverra accumsan in nisl nisi scelerisque eu. Diam donec adipiscing tristique risus. Arcu cursus euismod quis viverra nibh cras pulvinar mattis nunc. At auctor urna nunc id. Orci nulla pellentesque dignissim enim sit amet. Morbi enim nunc faucibus a. Sed enim ut sem viverra aliquet eget sit. Euismod in pellentesque massa placerat duis ultricies lacus sed. Sagittis orci a scelerisque purus. Feugiat nibh sed pulvinar proin gravida hendrerit lectus a. Sed arcu non odio euismod lacinia at quis risus. Senectus et netus et malesuada fames ac turpis egestas.

Scelerisque varius morbi enim nunc faucibus a pellentesque sit amet. Aliquam id diam maecenas ultricies mi. Felis imperdiet proin fermentum leo. Dictum fusce ut placerat orci nulla. Nibh ipsum consequat nisl vel pretium lectus quam id leo. Nunc non blandit massa enim nec. Sed enim ut sem viverra aliquet eget. Ac turpis egestas integer eget aliquet nibh. Sed risus pretium quam vulputate dignissim suspendisse in. Ornare arcu dui vivamus arcu. Dignissim cras tincidunt lobortis feugiat. Cum sociis natoque penatibus et magnis dis parturient montes. Elementum nisi quis eleifend quam adipiscing vitae. Auctor eu augue ut lectus arcu bibendum at. Id porta nibh venenatis cras sed. Pellentesque dignissim enim sit amet venenatis. Non enim praesent elementum facilisis leo vel fringilla est. Vestibulum rhoncus est pellentesque elit ullamcorper.

Volutpat blandit aliquam etiam erat velit. Diam donec adipiscing tristique risus nec feugiat in. Sem viverra aliquet eget sit amet tellus. Nunc non blandit massa enim nec. Nunc lobortis mattis aliquam faucibus purus in massa tempor. Mauris commodo quis imperdiet massa tincidunt nunc. Amet consectetur adipiscing elit ut aliquam. Vitae et leo duis ut diam quam nulla porttitor. Amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et. Vitae aliquet nec ullamcorper sit amet risus nullam. Eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis. At risus viverra adipiscing at in tellus integer feugiat. Non arcu risus quis varius quam quisque id diam. Turpis in eu mi bibendum neque egestas. Auctor eu augue ut lectus arcu bibendum at.

Lectus magna fringilla urna porttitor rhoncus dolor purus non enim. Sed libero enim sed faucibus turpis in eu mi bibendum. Ullamcorper velit sed ullamcorper morbi tincidunt ornare. Dolor sit amet consectetur adipiscing elit ut aliquam purus. Nullam non nisi est sit. Dui nunc mattis enim ut tellus elementum sagittis. Interdum consectetur libero id faucibus nisl tincidunt eget. Dolor magna eget est lorem ipsum dolor sit. Ultrices vitae auctor eu augue. Sed egestas egestas fringilla phasellus faucibus scelerisque eleifend. Scelerisque purus semper eget duis at tellus at. Fermentum iaculis eu non diam phasellus vestibulum lorem. Laoreet id donec ultrices tincidunt arcu non sodales neque sodales.`;
