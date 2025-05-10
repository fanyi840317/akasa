// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import { EditorProvider } from "./EditorProvider";
import EditorContainer from "./EditorContainer";
import "./App.css";

function App() {
  // const [count, setCount] = useState(0)

  return (
     <EditorProvider>
        <div className="app">
        <EditorContainer />
        </div>
      </EditorProvider>
  );
}

export default App;
