import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const TransferDetails = () => {
  const { transfer_id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [transfer, setTransfer] = useState(null);
  const [reversing, setReversing] = useState(false);
  const [reverseSuccess, setReverseSuccess] = useState(false);

  // Fetch transfer details
  useEffect(() => {
    const fetchTransfer = async () => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:8000/transfers/${transfer_id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка при получении данных о переводе");
        }

        const data = await response.json();
        setTransfer(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTransfer();
  }, [transfer_id, reverseSuccess]);

  const handleReverseTransfer = async () => {
    if (!window.confirm("Вы уверены, что хотите отменить этот перевод?")) return;

    try {
      setReversing(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/transfers/${transfer_id}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка при отмене перевода");
      }

      const data = await response.json();
      setTransfer(data);
      setReverseSuccess(true);
      alert("Перевод успешно отменён!");
    } catch (err) {
      setError(err.message);
    } finally {
      setReversing(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 max-w-2xl mx-auto">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Назад
        </button>
      </div>
    );
  }

  if (!transfer) return null;

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Детали перевода #{transfer.id}</h1>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
        >
          Назад
        </button>
      </div>

      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h2 className="text-lg font-medium mb-2">Отправитель</h2>
            <p className="text-gray-700">Счёт: {transfer.from_account_id}</p>
          </div>

          <div>
            <h2 className="text-lg font-medium mb-2">Получатель</h2>
            <p className="text-gray-700">Счёт: {transfer.to_account_id}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <h2 className="text-lg font-medium mb-2">Сумма</h2>
            <p className="text-gray-700">{transfer.amount} RUB</p>
          </div>

          <div>
            <h2 className="text-lg font-medium mb-2">Статус</h2>
            <p
              className={`font-medium ${
                transfer.status === "COMPLETED"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {transfer.status === "COMPLETED" ? "Выполнен" : "Отменён"}
            </p>
          </div>

          <div>
            <h2 className="text-lg font-medium mb-2">Дата создания</h2>
            <p className="text-gray-700">
              {new Date(transfer.created_at).toLocaleString()}
            </p>
          </div>
        </div>

        {transfer.status === "COMPLETED" && (
          <div className="flex justify-end">
            <button
              onClick={handleReverseTransfer}
              disabled={reversing}
              className={`px-4 py-2 rounded-lg text-white ${
                reversing
                  ? "bg-gray-400"
                  : "bg-red-500 hover:bg-red-600"
              }`}
            >
              {reversing ? "Отмена..." : "Отменить перевод"}
            </button>
          </div>
        )}

        {reverseSuccess && (
          <div className="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            Перевод успешно отменён!
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
    </div>
  );
};

export default TransferDetails;