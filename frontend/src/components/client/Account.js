import { useState, useEffect } from "react";

const accountTypeLabels = {
  SALARY: "Зарплатный",
  DEPOSIT: "Депозитный",
  SETTLEMENT: "Расчётный",
  LOAN: "Кредитный",
};

const Accounts = () => {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newAccountBankId, setNewAccountBankId] = useState("");
  const [isEditing, setIsEditing] = useState(null);
  const [updatedStatus, setUpdatedStatus] = useState("");

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:8000/profile/accounts", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) throw new Error("Ошибка загрузки счетов");
        const data = await response.json();
        setAccounts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAccounts();
  }, []);

  const handleCreateAccount = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("http://localhost:8000/profile/accounts", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bank_id: parseInt(newAccountBankId, 10),
        }),
      });

      if (!response.ok) throw new Error("Ошибка создания счета");
      
      const data = await response.json();
      setAccounts([...accounts, data]);
      setIsCreating(false);
      setNewAccountBankId("");
      alert("Счет успешно создан!");
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateAccount = async (accountId) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(`http://localhost:8000/profile/accounts/${accountId}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          status: updatedStatus,
        }),
      });

      if (!response.ok) throw new Error("Ошибка обновления счета");
      
      const data = await response.json();
      setAccounts(accounts.map(acc => acc.id === accountId ? data : acc));
      setIsEditing(null);
      setUpdatedStatus("");
      alert("Статус счета успешно обновлен!");
    } catch (err) {
      setError(err.message);
    }
  };

  // Удалена функция handleDeleteAccount

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Счета</h1>

      {isCreating ? (
        <div className="mb-4">
          <label htmlFor="bankId" className="block text-gray-700">ID банка</label>
          <input
            type="number"
            id="bankId"
            value={newAccountBankId}
            onChange={(e) => setNewAccountBankId(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg"
          />
          <button
            onClick={handleCreateAccount}
            className="bg-green-500 text-white p-2 rounded-lg mt-2 hover:bg-green-600"
          >
            Создать счет
          </button>
          <button
            onClick={() => setIsCreating(false)}
            className="bg-gray-500 text-white p-2 rounded-lg mt-2 ml-2 hover:bg-gray-600"
          >
            Отмена
          </button>
        </div>
      ) : (
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white p-2 rounded-lg mb-4 hover:bg-blue-600"
        >
          Создать новый счет
        </button>
      )}

      <div className="space-y-4">
        {accounts.map((account) => (
          <div key={account.id} className="p-4 border border-gray-300 rounded-lg">
            <p><strong>Тип счета:</strong> {accountTypeLabels[account.type] || account.type}</p>
            <p><strong>ID счета:</strong> {account.id}</p>
            <p><strong>ID пользователя:</strong> {account.user_id}</p>
            <p><strong>ID банка:</strong> {account.bank_id}</p>
            <p><strong>Баланс:</strong> {account.balance}</p>
            <p><strong>Статус:</strong> {account.status}</p>
            <p><strong>Создан:</strong> {new Date(account.created_at).toLocaleString()}</p>
            <p><strong>Обновлен:</strong> {new Date(account.updated_at).toLocaleString()}</p>

            {isEditing === account.id ? (
              <div className="mt-2">
                <label htmlFor="status" className="block text-gray-700">Новый статус</label>
                <input
                  type="text"
                  id="status"
                  value={updatedStatus}
                  onChange={(e) => setUpdatedStatus(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
                <button
                  onClick={() => handleUpdateAccount(account.id)}
                  className="bg-green-500 text-white p-2 rounded-lg mt-2 hover:bg-green-600"
                >
                  Сохранить
                </button>
                <button
                  onClick={() => setIsEditing(null)}
                  className="bg-gray-500 text-white p-2 rounded-lg mt-2 ml-2 hover:bg-gray-600"
                >
                  Отмена
                </button>
              </div>
            ) : (
              <button
                onClick={() => setIsEditing(account.id)}
                className="bg-yellow-500 text-white p-2 rounded-lg mt-2 hover:bg-yellow-600"
              >
                Изменить статус
              </button>
            )}

            {/* Удалена кнопка удаления счета */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Accounts;