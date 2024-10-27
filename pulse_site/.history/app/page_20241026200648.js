"use client"; // Enables client-side features like hooks

import { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [companyType, setCompanyType] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle the form submission, e.g., send data to API or log it
    console.log({ email, companyName, companyType });
  };

  const handleSelectType = (type) => {
    setCompanyType(type);
    setIsOpen(false); // Close dropdown after selection
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-black">Pulse</h2>

        <div className="mb-4"> 
          <label className="block text-gray-700">Email</label>
          <input
            type="email"
            placeholder="adam@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-2 p-2 w-full border rounded font-medium text-black"
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Company Name</label>
          <input
            type="text"
            placeholder="Company X"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            className="mt-2 p-2 w-full border rounded font-medium text-black"
            required
          />
        </div>

        <div className="mb-4"> 
          <label className="block text-gray-700">Company Type</label>

          <div className="relative">
            <button
              type="button"
              className="flex w-full items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              id="menu-button"
              aria-expanded={isOpen}
              aria-haspopup="true"
              onClick={() => setIsOpen((prev) => !prev)} // Toggle dropdown
            >
              <span className="flex-grow text-left">{companyType || "Select Type"}</span>
              <svg
                className="h-5 w-5 text-gray-400"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
                  clipRule="evenodd"
                />
              </svg>
            </button>



            {isOpen && (
              <div className="absolute left-0 z-10 mt-2 w-56 origin-top-left divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              role="menu" aria-orientation="vertical" aria-labelledby="menu-button">
                <div className="py-1" role="none">
                  <button onClick={() => handleSelectType('vendor')} className="block px-4 py-2 text-sm text-gray-700 w-full text-left" role="menuitem">
                    Vendor
                  </button>
                  <button onClick={() => handleSelectType('seller')} className="block px-4 py-2 text-sm text-gray-700 w-full text-left" role="menuitem">
                    Seller
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        

        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded mt-4 hover:bg-blue-600"
        >
          Submit
        </button>
      </form>
    </div>
  );
}
