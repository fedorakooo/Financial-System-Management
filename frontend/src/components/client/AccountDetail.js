import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const AccountDetails = () => {
  const { accountId } = useParams();
  const numericAccountId = Number(accountId);
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isNaN(numericAccountId) || numericAccountId <= 0) {
      setError("❌ Некорректный идентификатор счета.");
      return;
    }

    const fetchAccountDetails = async () => {
      try {
        setLoading(true);
        setError(null);
        const token = localStorage.getItem("access_token");

        const response = await fetch(
          `http://localhost:8000/profile/accounts/${numericAccountId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          if (response.status === 401) throw new Error("❌ Неверный или просроченный токен.");
          if (response.status === 403) throw new Error("❌ Учетная запись неактивна.");
          if (response.status === 404) throw new Error("❌ Счет не найден.");
          if (response.status === 500) throw new Error("🚨 Внутренняя ошибка сервера.");
          throw new Error("Ошибка загрузки данных счета.");
        }

        const data = await response.json();
        setAccount(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAccountDetails();
  }, [numericAccountId]);

  if (loading) return <p>⏳ Загрузка...</p>;
  if (error) return <p style={{ color: "red", fontWeight: "bold" }}>{error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">
        📜 Информация о счете #{numericAccountId}
      </h1>
      <Link
        to="/profile/accounts"
        className="bg-gray-500 text-white p-2 rounded-lg hover:bg-gray-600 mb-4 block"
      >
        ⬅️ Перейти к списку счетов
      </Link>

      {account ? (
        <div className="border p-4 rounded-lg">
          <p><strong>🆔 ID:</strong> {account.id}</p>
          <p><strong>👤 Пользователь ID:</strong> {account.user_id}</p>
          <p><strong>🏦 Банк ID:</strong> {account.bank_id}</p>
          <p><strong>💰 Баланс:</strong> {account.balance} ₽</p>
          <p><strong>🔹 Статус:</strong> {account.status}</p>
          <p><strong>💳 Тип счета:</strong> {account.type}</p>
          <p><strong>📅 Дата создания:</strong> {new Date(account.created_at).toLocaleString("ru-RU")}</p>
          <p><strong>📅 Дата обновления:</strong> {new Date(account.updated_at).toLocaleString("ru-RU")}</p>
        </div>
      ) : (
        <p>📭 Нет данных для отображения</p>
      )}
    </div>
  );
};

export default AccountDetails;
