import { useEffect, useState } from "react";

const BankList = () => {
  const [banks, setBanks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBanks = async () => {
      try {
        const response = await fetch("http://localhost:8000/banks");
        if (!response.ok) {
          throw new Error("Ошибка загрузки данных");
        }
        const data = await response.json();
        setBanks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBanks();
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
      {banks.map((bank, index) => (
        <div key={bank.id}>
          <div
            className="border border-gray-300 p-4 rounded-lg shadow-md hover:shadow-lg transition transform hover:scale-105 bg-white"
          >
            <h3 className="text-lg font-semibold mb-2 text-gray-800">{bank.name}</h3>
            <p><strong>ID:</strong> {bank.id}</p>
            <p><strong>BIC:</strong> {bank.bic}</p>
            <p><strong>Адрес:</strong> {bank.address}</p>
            <p><strong>Создан:</strong> {new Date(bank.created_at).toLocaleString()}</p>
            <p><strong>Обновлён:</strong> {new Date(bank.updated_at).toLocaleString()}</p>
          </div>

          {index < banks.length - 1 && (
            <hr className="my-4 border-t-2 border-gray-300" />
          )}
        </div>
      ))}
    </div>
  );
};

export default BankList;
