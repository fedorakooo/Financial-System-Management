import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";

const Additions = () => {
  const [searchParams] = useSearchParams();
  const accountId = searchParams.get("account_id");
  const [additions, setAdditions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newAddition, setNewAddition] = useState({
    amount: "",
    source: "CASH",
  });

  // Загрузка добавлений
  useEffect(() => {
    const fetchAdditions = async () => {
      try {
        setLoading(true);
        setError(null);
        
        if (!accountId || isNaN(accountId)) {
          throw new Error("Неверный идентификатор счета");
        }

        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:8000/profile/accounts/additions/?account_id=${accountId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка загрузки добавлений");
        }

        const data = await response.json();
        setAdditions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAdditions();
  }, [accountId]);

  // Создание добавления
  const handleCreateAddition = async () => {
    try {
      if (!accountId || isNaN(accountId)) {
        throw new Error("Неверный идентификатор счета");
      }

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/profile/accounts/additions/?account_id=${accountId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: parseFloat(newAddition.amount),
            source: newAddition.source,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка создания добавления");
      }

      const data = await response.json();
      setAdditions([...additions, data]);
      setIsCreating(false);
      setNewAddition({ amount: "", source: "CASH" });
      alert("Добавление успешно создано!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Добавления к счету #{accountId}</h1>

      {/* Кнопка создания */}
      {!isCreating && (
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white p-2 rounded-lg mb-4 hover:bg-blue-600"
        >
          Создать новое добавление
        </button>
      )}

      {/* Форма создания */}
      {isCreating && (
        <div className="mb-4 p-4 border border-gray-300 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">Новое добавление</h2>
          
          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Сумма</label>
            <input
              type="number"
              step="0.01"
              value={newAddition.amount}
              onChange={(e) => setNewAddition({...newAddition, amount: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите сумму"
            />
          </div>

          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Источник</label>
            <select
              value={newAddition.source}
              onChange={(e) => setNewAddition({...newAddition, source: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg"
            >
              <option value="CASH">Наличные</option>
              <option value="BANK_TRANSFER">Банковский перевод</option>
              <option value="OTHER">Другое</option>
            </select>
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleCreateAddition}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Создать
            </button>
            <button
              onClick={() => setIsCreating(false)}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
            >
              Отмена
            </button>
          </div>
        </div>
      )}

      {/* Список добавлений */}
      <div className="space-y-4">
        {additions.map((addition) => (
          <div key={addition.id} className="p-4 border border-gray-300 rounded-lg">
            <p><strong>ID:</strong> {addition.id}</p>
            <p><strong>Сумма:</strong> {addition.amount}</p>
            <p><strong>Источник:</strong> {addition.source}</p>
            <p><strong>Дата создания:</strong> {new Date(addition.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>

      {/* Сообщение при пустом списке */}
      {additions.length === 0 && !isCreating && (
        <p className="text-gray-500">Нет добавлений для этого счета</p>
      )}
    </div>
  );
};

export default Additions;