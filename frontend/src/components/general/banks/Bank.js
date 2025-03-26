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

  if (loading) return <p style={styles.loadingText}>Загрузка...</p>;
  if (error) return <p style={styles.errorText}>Ошибка: {error}</p>;

  return (
    <div style={styles.container}>
      {bank && (
        <div style={styles.bankCard}>
          <h3 style={styles.bankTitle}>{bank.name}</h3>
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

const styles = {
  container: {
    padding: "20px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "#f7fafc",
  },
  bankCard: {
    width: "100%",
    maxWidth: "600px",
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    border: "1px solid #e2e8f0",
  },
  bankTitle: {
    fontSize: "24px",
    fontWeight: "bold",
    color: "#333",
    marginBottom: "15px",
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
};

export default GeneralBank;
