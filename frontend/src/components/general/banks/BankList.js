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

  if (loading) return <p style={styles.loadingText}>Загрузка...</p>;
  if (error) return <p style={styles.errorText}>Ошибка: {error}</p>;

  return (
    <div style={styles.container}>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
        {banks.map((bank, index) => (
          <div key={bank.id}>
            <div style={styles.bankCard} className="transition-transform hover:scale-105">
              <h3 style={styles.bankTitle}>{bank.name}</h3>
              <p><strong>ID:</strong> {bank.id}</p>
              <p><strong>BIC:</strong> {bank.bic}</p>
              <p><strong>Адрес:</strong> {bank.address}</p>
              <p><strong>Создан:</strong> {new Date(bank.created_at).toLocaleString()}</p>
              <p><strong>Обновлён:</strong> {new Date(bank.updated_at).toLocaleString()}</p>
            </div>

            {index < banks.length - 1 && <hr style={styles.hr} />}
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: "20px",
    backgroundColor: "#f7fafc",
  },
  loadingText: {
    fontSize: "18px",
    color: "#4a90e2",
    textAlign: "center",
  },
  errorText: {
    fontSize: "18px",
    color: "red",
    textAlign: "center",
  },
  bankCard: {
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    border: "1px solid #e2e8f0",
    transition: "box-shadow 0.3s ease",
    cursor: "pointer",
  },
  bankTitle: {
    fontSize: "20px",
    fontWeight: "bold",
    color: "#333",
    marginBottom: "15px",
  },
  hr: {
    margin: "20px 0",
    borderTop: "2px solid #e2e8f0",
  },
};

export default BankList;
