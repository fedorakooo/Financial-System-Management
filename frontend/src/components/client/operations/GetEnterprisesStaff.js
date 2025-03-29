import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const GetEnterprise = () => {
  const { enterpriseId } = useParams();
  const navigate = useNavigate();
  const [enterprise, setEnterprise] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEnterprise = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const id = parseInt(enterpriseId, 10); // Явное преобразование в число

        if (isNaN(id)) {
          throw new Error("Некорректный ID предприятия");
        }

        const response = await fetch(`http://localhost:8000/staff/enterprises/${id}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Ошибка при загрузке предприятия");
        }

        const data = await response.json();
        setEnterprise(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchEnterprise();
  }, [enterpriseId]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold">Данные предприятия</h1>
      {error && <p className="text-red-500">Ошибка: {error}</p>}
      {enterprise ? (
        <div className="border p-4 mt-4">
          <p><strong>ID:</strong> {enterprise.id}</p>
          <p><strong>Название:</strong> {enterprise.name}</p>
          <p><strong>Тип:</strong> {enterprise.type}</p>
          <p><strong>УНП:</strong> {enterprise.unp}</p>
          <p><strong>Банк ID:</strong> {enterprise.bank_id}</p>
          <p><strong>Адрес:</strong> {enterprise.address}</p>
        </div>
      ) : (
        <p>Загрузка...</p>
      )}
      <button onClick={() => navigate(-1)} className="mt-4 bg-blue-500 text-white p-2 rounded">Назад</button>
    </div>
  );
};

export default GetEnterprise;
