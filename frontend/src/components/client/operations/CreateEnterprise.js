import { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateEnterprise = () => {
  const [name, setName] = useState("");
  const [type, setType] = useState("LLC"); // Значение по умолчанию
  const [unp, setUnp] = useState("");
  const [bankId, setBankId] = useState("");
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const token = localStorage.getItem("access_token");
    const enterpriseData = {
      name,
      type,
      unp,
      bank_id: parseInt(bankId),
      address,
    };

    try {
      const response = await fetch("http://localhost:8000/staff/enterprises/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(enterpriseData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка при создании предприятия");
      }

      const data = await response.json();
      navigate(`/enterprises/${data.id}`); // Перенаправление на страницу предприятия
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold">Создать предприятие</h1>
      {error && <p className="text-red-500">Ошибка: {error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block">Название</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Тип предприятия</label>
          <select value={type} onChange={(e) => setType(e.target.value)} className="border p-2 w-full">
            <option value="LLC">LLC</option>
            <option value="SP">SP</option>
            <option value="LLP">LLP</option>
          </select>
        </div>
        <div>
          <label className="block">УНП</label>
          <input type="text" value={unp} onChange={(e) => setUnp(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Банк ID</label>
          <input type="number" value={bankId} onChange={(e) => setBankId(e.target.value)} className="border p-2 w-full" required />
        </div>
        <div>
          <label className="block">Адрес</label>
          <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} className="border p-2 w-full" required />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded" disabled={loading}>
          {loading ? "Создание..." : "Создать"}
        </button>
      </form>
    </div>
  );
};

export default CreateEnterprise;
