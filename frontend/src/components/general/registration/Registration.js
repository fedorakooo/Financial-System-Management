import { useState } from "react";

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    passport_number: "",
    phone_number: "",
    email: "",
    password: "",
    role: "USER",
    is_foreign: false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setUserData(null);

    try {
      const response = await fetch("http://localhost:8000/registration/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        if (response.status === 409) {
          throw new Error("Пользователь с таким номером уже существует.");
        }
        throw new Error("Ошибка при регистрации. Попробуйте позже.");
      }

      const data = await response.json();
      setUserData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Styles
  const containerStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f0f2f5",
  };

  const formContainerStyle = {
    padding: "30px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    width: "100%",
    maxWidth: "500px",
    backgroundColor: "#fff",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  };

  const headingStyle = {
    textAlign: "center",
    marginBottom: "20px",
    fontSize: "24px",
    color: "#333",
  };

  const labelStyle = {
    display: "block",
    marginBottom: "8px",
    fontWeight: "bold",
    color: "#333",
  };

  const inputStyle = {
    width: "100%",
    padding: "12px",
    marginBottom: "15px",
    borderRadius: "4px",
    border: "1px solid #ccc",
    fontSize: "16px",
    color: "#333",
  };

  const buttonStyle = {
    width: "100%",
    padding: "12px",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "16px",
    transition: "background-color 0.3s ease",
  };

  const buttonHoverStyle = {
    backgroundColor: "#0056b3",
  };

  const errorStyle = {
    color: "red",
    fontSize: "14px",
    textAlign: "center",
    marginTop: "10px",
  };

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <h2 style={headingStyle}>Регистрация</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="name" style={labelStyle}>Имя</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              style={inputStyle}
            />
          </div>

          <div>
            <label htmlFor="passport_number" style={labelStyle}>Паспорт</label>
            <input
              type="text"
              name="passport_number"
              value={formData.passport_number}
              onChange={handleChange}
              required
              style={inputStyle}
            />
          </div>

          <div>
            <label htmlFor="phone_number" style={labelStyle}>Телефон</label>
            <input
              type="text"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              required
              style={inputStyle}
            />
          </div>

          <div>
            <label htmlFor="email" style={labelStyle}>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              style={inputStyle}
            />
          </div>

          <div>
            <label htmlFor="password" style={labelStyle}>Пароль</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={inputStyle}
            />
          </div>

          <div style={{ display: "flex", alignItems: "center", marginBottom: "20px" }}>
            <input
              type="checkbox"
              name="is_foreign"
              checked={formData.is_foreign}
              onChange={handleChange}
              style={{ marginRight: "8px" }}
            />
            <label style={{ fontSize: "16px" }}>Иностранный пользователь</label>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={buttonStyle}
            onMouseEnter={(e) => e.target.style.backgroundColor = buttonHoverStyle.backgroundColor}
            onMouseLeave={(e) => e.target.style.backgroundColor = '#007bff'}
          >
            {loading ? "Регистрация..." : "Зарегистрироваться"}
          </button>
        </form>

        {error && <p style={errorStyle}>{error}</p>}

        {userData && (
          <div style={{ marginTop: "20px", padding: "15px", backgroundColor: "#d4edda", borderRadius: "5px" }}>
            <h3 style={{ fontWeight: "bold" }}>Регистрация успешна!</h3>
            <p><strong>ID:</strong> {userData.id}</p>
            <p><strong>Имя:</strong> {userData.name}</p>
            <p><strong>Паспорт:</strong> {userData.passport_number}</p>
            <p><strong>Телефон:</strong> {userData.phone_number}</p>
            <p><strong>Email:</strong> {userData.email}</p>
            <p><strong>Роль:</strong> {userData.role}</p>
            <p><strong>Активен:</strong> {userData.is_active ? "Да" : "Нет"}</p>
            <p><strong>Иностранец:</strong> {userData.is_foreign ? "Да" : "Нет"}</p>
            <p><strong>Создан:</strong> {new Date(userData.created_at).toLocaleString()}</p>
            <p><strong>Обновлен:</strong> {new Date(userData.updated_at).toLocaleString()}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Register;
