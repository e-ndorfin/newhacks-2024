"use client"; // Enables client-side features like hooks

import { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [companyType, setCompanyType] = useState('');
  const [state, setState] = useState('');
  const [isCompanyTypeOpen, setIsCompanyTypeOpen] = useState(false); // Separate state for company type dropdown
  const [isStateOpen, setIsStateOpen] = useState(false); // Separate state for states dropdown

  const companyTypes = {
    vendor: "Vendor",
    ngo: "Non-governmental Organization",
    seller: "Seller", // Add more entries here if needed
  };

  const states = {
    AL: "Alabama",
    AK: "Alaska",
    AZ: "Arizona",
    AR: "Arkansas",
    CA: "California",
    CO: "Colorado",
    CT: "Connecticut",
    DE: "Delaware",
    FL: "Florida",
    GA: "Georgia",
    HI: "Hawaii",
    ID: "Idaho",
    IL: "Illinois",
    IN: "Indiana",
    IA: "Iowa",
    KS: "Kansas",
    KY: "Kentucky",
    LA: "Louisiana",
    ME: "Maine",
    MD: "Maryland",
    MA: "Massachusetts",
    MI: "Michigan",
    MN: "Minnesota",
    MS: "Mississippi",
    MO: "Missouri",
    MT: "Montana",
    NE: "Nebraska",
    NV: "Nevada",
    NH: "New Hampshire",
    NJ: "New Jersey",
    NM: "New Mexico",
    NY: "New York",
    NC: "North Carolina",
    ND: "North Dakota",
    OH: "Ohio",
    OK: "Oklahoma",
    OR: "Oregon",
    PA: "Pennsylvania",
    RI: "Rhode Island",
    SC: "South Carolina",
    SD: "South Dakota",
    TN: "Tennessee",
    TX: "Texas",
    UT: "Utah",
    VT: "Vermont",
    VA: "Virginia",
    WA: "Washington",
    WV: "West Virginia",
    WI: "Wisconsin",
    WY: "Wyoming",
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle the form submission, e.g., send data to API or log it
    console.log({ email, companyName, companyType, state });
  };

  const handleSelectType = (type) => {
    setCompanyType(type);
    setIsCompanyTypeOpen(false); // Close company type dropdown after selection
  };

  const handleSelectState = (abbreviation) => {
    setState(abbreviation);
    setIsStateOpen(false); // Close states dropdown after selection
  };

  const capitalizeFirstLetter = (str) => { 
    return str 
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
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
            className="mt-2 p-2 w-full border rounded font-semibold text-black"
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
            className="mt-2 p-2 w-full border rounded font-semibold text-black"
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
              aria-expanded={isCompanyTypeOpen}
              aria-haspopup="true"
              onClick={() => setIsCompanyTypeOpen((prev) => !prev)} // Toggle company type dropdown
            >
              <span className="flex-grow text-left">{companyType ? capitalizeFirstLetter(companyType) : ""}</span>
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

            {isCompanyTypeOpen && (
              <div
                className="absolute left-0 z-10 mt-2 w-56 origin-top-left divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="menu-button"
              >
                <div className="py-1" role="none">
                  {Object.entries(companyTypes).map(([key, value]) => (
                    <button
                      key={key} // Use the key as a unique identifier
                      onClick={() => handleSelectType(key)} // Pass the key to the handler
                      className="block px-4 py-2 text-sm text-gray-700 w-full text-left"
                      role="menuitem"
                    >
                      {value} {/* Display the value */}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mb-4"> 
          <label className="block text-gray-700">States</label>

          <div className="relative">
            <button
              type="button"
              className="flex w-full items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              id="menu-button"
              aria-expanded={isStateOpen}
              aria-haspopup="true"
              onClick={() => setIsStateOpen((prev) => !prev)} // Toggle states dropdown
            >
              <span className="flex-grow text-left">{state ? states[state] : ""}</span>
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

            {isStateOpen && (
              <div
                className="absolute left-0 z-10 mt-2 w-56 origin-top-left divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none max-h-40 overflow-y-auto" // Reduced max height for scrolling
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="menu-button"
              >
                <div className="py-1" role="none">
                  {Object.entries(states).map(([key, value]) => (
                    <button
                      key={key} // Use the key as a unique identifier
                      onClick={() => handleSelectState(key)} // Pass the key to the handler
                      className="block px-4 py-2 text-sm text-gray-700 w-full text-left"
                      role="menuitem"
                    >
                      {value} {/* Display the value */}
                    </button>
                  ))}
                </div>
              </div>
            )}

          </div>
        </div>

        <button
          type="submit"
          className="mt-4 w-full rounded bg-blue-600 py-2 text-white font-semibold hover:bg-blue-700"
        >
          Submit
        </button>
      </form>
    </div>
  );
}
