import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

const GeneralBank = () => {
  const { bankId } = useParams(); // Get the bank ID from the URL
  const [bank, setBank] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBank = async () => {
      try {
        const response = await fetch(`http://localhost:8000/banks/${bankId}`);
        if (!response.ok) {
          throw new Error("Ошибка загрузки данных");
        }
        const data = await response.json();
        setBank(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (bankId) {
      fetchBank();
    }
  }, [bankId]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      {bank && (
        <div className="border border-gray-300 p-4 rounded-lg shadow-md bg-white">
          <h3 className="text-2xl font-semibold text-gray-800">{bank.name}</h3>
          <p><strong>ID:</strong> {bank.id}</p>
          <p><strong>BIC:</strong> {bank.bic}</p>
          <p><strong>Адрес:</strong> {bank.address}</p>
          <p><strong>Создан:</strong> {new Date(bank.created_at).toLocaleString()}</p>
          <p><strong>Обновлён:</strong> {new Date(bank.updated_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default GeneralBank;
