import { useEffect, useState } from "react";
import axios from "axios";
import Tree from "react-d3-tree";

export default function App() {
  const [entities, setEntities] = useState([]);
  const [newEntityName, setNewEntityName] = useState("");
  const backendUrl = "http://localhost:8000";

  useEffect(() => { fetchEntities(); }, []);

  const fetchEntities = async () => {
    const res = await axios.get(`${backendUrl}/entities`);
    setEntities(res.data);
  };

  const createEntity = async () => {
    await axios.post(`${backendUrl}/entities`, {
      name: newEntityName,
      type: "student",
      attributes: {},
      emotions: {},
      additional: {},
      children: []
    });
    setNewEntityName("");
    fetchEntities();
  };

  const formatTree = (entities) =>
    entities.map((e) => ({
      name: e.name,
      attributes: e.attributes,
      children: e.children ? formatTree(e.children) : []
    }));

  return (
    <div style={{ width: "100%", height: "100vh", padding: 20 }}>
      <h1>SCTM Live Universe</h1>
      <input
        value={newEntityName}
        onChange={(e) => setNewEntityName(e.target.value)}
        placeholder="New entity name"
      />
      <button onClick={createEntity}>Create</button>
      <div style={{ width: "100%", height: "80vh" }}>
        <Tree data={formatTree(entities)} orientation="vertical" />
      </div>
    </div>
  );
}
