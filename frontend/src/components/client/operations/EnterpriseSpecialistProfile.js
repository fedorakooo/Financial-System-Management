// components/EnterpriseSpecialistProfile.js
import { useState, useEffect } from "react";

const EnterpriseSpecialistProfile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:8000/enterprises/specialists/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) throw new Error("Ошибка загрузки профиля");
        
        setProfile(await response.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Профиль специалиста</h1>
      <p><strong>ID:</strong> {profile.id}</p>
      <p><strong>Предприятие:</strong> {profile.enterprise.name}</p>
    </div>
  );
};

export default EnterpriseSpecialistProfile;
