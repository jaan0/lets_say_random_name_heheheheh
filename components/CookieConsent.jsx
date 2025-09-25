import React, { useState, useEffect } from 'react';
import { X, Cookie, Settings, Shield, BarChart3 } from 'lucide-react';
import Cookies from 'js-cookie';

const CookieConsent = () => {
  const [showBanner, setShowBanner] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [preferences, setPreferences] = useState({
    necessary: true, // Always true, can't be disabled
    analytics: false,
    marketing: false,
    functional: false
  });

  useEffect(() => {
    // Check if user has already made a choice
    const consent = Cookies.get('cookie-consent');
    if (!consent) {
      setShowBanner(true);
    } else {
      // Load saved preferences
      const savedPrefs = Cookies.get('cookie-preferences');
      if (savedPrefs) {
        setPreferences(JSON.parse(savedPrefs));
      }
    }
  }, []);

  const handleAcceptAll = () => {
    const allAccepted = {
      necessary: true,
      analytics: true,
      marketing: true,
      functional: true
    };
    
    setPreferences(allAccepted);
    savePreferences(allAccepted);
    setShowBanner(false);
  };

  const handleRejectAll = () => {
    const onlyNecessary = {
      necessary: true,
      analytics: false,
      marketing: false,
      functional: false
    };
    
    setPreferences(onlyNecessary);
    savePreferences(onlyNecessary);
    setShowBanner(false);
  };

  const handleSavePreferences = () => {
    savePreferences(preferences);
    setShowBanner(false);
    setShowSettings(false);
  };

  const savePreferences = (prefs) => {
    Cookies.set('cookie-consent', 'true', { expires: 365 });
    Cookies.set('cookie-preferences', JSON.stringify(prefs), { expires: 365 });
    
    // Set individual cookies based on preferences
    if (prefs.analytics) {
      Cookies.set('analytics-enabled', 'true', { expires: 365 });
    } else {
      Cookies.remove('analytics-enabled');
    }
    
    if (prefs.marketing) {
      Cookies.set('marketing-enabled', 'true', { expires: 365 });
    } else {
      Cookies.remove('marketing-enabled');
    }
    
    if (prefs.functional) {
      Cookies.set('functional-enabled', 'true', { expires: 365 });
    } else {
      Cookies.remove('functional-enabled');
    }
  };

  const togglePreference = (key) => {
    if (key === 'necessary') return; // Can't disable necessary cookies
    
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  if (!showBanner) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-50 z-40" />
      
      {/* Cookie Banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
        <div className="max-w-7xl mx-auto p-4">
          {!showSettings ? (
            // Main banner
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-start gap-3">
                <Cookie className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">
                    We use cookies to improve your experience
                  </h3>
                  <p className="text-sm text-gray-600">
                    We use cookies to analyze website performance, remember your preferences, 
                    and provide personalized content. You can customize your cookie preferences below.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-2 w-full md:w-auto">
                <button
                  onClick={() => setShowSettings(true)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  <Settings className="w-4 h-4 inline mr-2" />
                  Customize
                </button>
                <button
                  onClick={handleRejectAll}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Reject All
                </button>
                <button
                  onClick={handleAcceptAll}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  Accept All
                </button>
              </div>
            </div>
          ) : (
            // Settings panel
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">
                  Cookie Preferences
                </h3>
                <button
                  onClick={() => setShowSettings(false)}
                  className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <div className="space-y-4">
                {/* Necessary Cookies */}
                <div className="flex items-start justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Shield className="w-5 h-5 text-green-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-gray-900">Necessary Cookies</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Essential for the website to function properly. These cannot be disabled.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <div className="w-10 h-6 bg-green-600 rounded-full flex items-center justify-end px-1">
                      <div className="w-4 h-4 bg-white rounded-full"></div>
                    </div>
                  </div>
                </div>

                {/* Analytics Cookies */}
                <div className="flex items-start justify-between p-4 bg-white border border-gray-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <BarChart3 className="w-5 h-5 text-blue-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-gray-900">Analytics Cookies</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Help us understand how visitors interact with our website by collecting anonymous information.
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => togglePreference('analytics')}
                    className={`w-10 h-6 rounded-full flex items-center px-1 transition-colors ${
                      preferences.analytics ? 'bg-blue-600 justify-end' : 'bg-gray-300 justify-start'
                    }`}
                  >
                    <div className="w-4 h-4 bg-white rounded-full"></div>
                  </button>
                </div>

                {/* Functional Cookies */}
                <div className="flex items-start justify-between p-4 bg-white border border-gray-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Settings className="w-5 h-5 text-purple-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-gray-900">Functional Cookies</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Enable enhanced functionality and personalization, such as remembering your preferences.
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => togglePreference('functional')}
                    className={`w-10 h-6 rounded-full flex items-center px-1 transition-colors ${
                      preferences.functional ? 'bg-blue-600 justify-end' : 'bg-gray-300 justify-start'
                    }`}
                  >
                    <div className="w-4 h-4 bg-white rounded-full"></div>
                  </button>
                </div>

                {/* Marketing Cookies */}
                <div className="flex items-start justify-between p-4 bg-white border border-gray-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Cookie className="w-5 h-5 text-orange-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-gray-900">Marketing Cookies</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Used to track visitors across websites to display relevant and engaging advertisements.
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => togglePreference('marketing')}
                    className={`w-10 h-6 rounded-full flex items-center px-1 transition-colors ${
                      preferences.marketing ? 'bg-blue-600 justify-end' : 'bg-gray-300 justify-start'
                    }`}
                  >
                    <div className="w-4 h-4 bg-white rounded-full"></div>
                  </button>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-2 pt-4 border-t border-gray-200">
                <button
                  onClick={handleRejectAll}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Reject All
                </button>
                <button
                  onClick={handleAcceptAll}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  Accept All
                </button>
                <button
                  onClick={handleSavePreferences}
                  className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                >
                  Save Preferences
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default CookieConsent;
